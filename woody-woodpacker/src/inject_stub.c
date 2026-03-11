#include "woody-woodpacker.h"
#include "stub_bytes.h"

/*
** find_last_segment_end — Devuelve la dirección virtual justo después
** del último PT_LOAD, alineada a página.
** Esto garantiza que el stub no colisiona con ningún segmento existente.
*/
static uint64_t	find_last_load_end(void *file)
{
	Elf64_Ehdr	*ehdr;
	Elf64_Phdr	*phdr;
	uint64_t	end;
	uint64_t	candidate;
	int			i;

	ehdr = (Elf64_Ehdr *)file;
	phdr = (Elf64_Phdr *)((char *)file + ehdr->e_phoff);
	end = 0;
	i = 0;
	while (i < ehdr->e_phnum)
	{
		if (phdr[i].p_type == PT_LOAD)
		{
			candidate = phdr[i].p_vaddr + phdr[i].p_memsz;
			if (candidate > end)
				end = candidate;
		}
		i++;
	}
	/* Alinear a la siguiente página */
	return ((end + 0xFFF) & ~(uint64_t)0xFFF);
}

/*
** find_pt_note — Busca el segmento PT_NOTE para convertirlo en PT_LOAD.
** Es la técnica de "PT_NOTE hijacking": el kernel ignora PT_NOTE en runtime,
** por lo que puede ser reutilizado para mapear nuestro stub.
*/
static Elf64_Phdr	*find_pt_note(void *file)
{
	Elf64_Ehdr	*ehdr;
	Elf64_Phdr	*phdr;
	int			i;

	ehdr = (Elf64_Ehdr *)file;
	phdr = (Elf64_Phdr *)((char *)file + ehdr->e_phoff);
	i = 0;
	while (i < ehdr->e_phnum)
	{
		if (phdr[i].p_type == PT_NOTE)
			return (&phdr[i]);
		i++;
	}
	return (NULL);
}

/*
** find_exec_segment — Localiza el segmento PT_LOAD ejecutable (.text).
** Necesitamos su vaddr y filesz para que el stub sepa qué desencriptar.
*/
static Elf64_Phdr	*find_exec_segment(void *file)
{
	Elf64_Ehdr	*ehdr;
	Elf64_Phdr	*phdr;
	int			i;

	ehdr = (Elf64_Ehdr *)file;
	phdr = (Elf64_Phdr *)((char *)file + ehdr->e_phoff);
	i = 0;
	while (i < ehdr->e_phnum)
	{
		if (phdr[i].p_type == PT_LOAD && (phdr[i].p_flags & PF_X))
			return (&phdr[i]);
		i++;
	}
	return (NULL);
}

/*
** patch_stub — Rellena los placeholders del bytecode del stub con
** los valores reales calculados en tiempo de ejecución de woody_woodpacker.
**
**  Offset 106 (0x6A): key        — 16 bytes XOR key
**  Offset 122 (0x7A): seg_addr   — uint64_t vaddr del segmento cifrado
**  Offset 130 (0x82): seg_size   — uint64_t tamaño del segmento cifrado
**  Offset 138 (0x8A): orig_entry — uint64_t entry point original del ELF
*/
static void	patch_stub(unsigned char *stub, uint64_t seg_addr,
						uint64_t seg_size, uint64_t orig_entry,
						unsigned char *key)
{
	memcpy(stub + STUB_KEY_OFFSET, key, KEY_SIZE);
	memcpy(stub + STUB_SEG_ADDR_OFFSET, &seg_addr, sizeof(uint64_t));
	memcpy(stub + STUB_SEG_SIZE_OFFSET, &seg_size, sizeof(uint64_t));
	memcpy(stub + STUB_ENTRY_OFFSET, &orig_entry, sizeof(uint64_t));
}

/*
** inject_stub — Inyecta el shellcode de desencriptación en el ELF.
**
** Proceso:
**  1. Localizar PT_NOTE → lo convertimos en PT_LOAD ejecutable
**  2. Localizar PT_LOAD ejecutable → obtenemos vaddr/filesz del segmento cifrado
**  3. Calcular dirección virtual del stub (al final del último PT_LOAD)
**  4. Parchear placeholders del stub con key, seg_addr, seg_size, orig_entry
**  5. Escribir stub al final del buffer (file_size original)
**  6. Modificar PT_NOTE→PT_LOAD apuntando al stub
**  7. Redirigir e_entry al inicio del stub
*/
int	inject_stub(void *file, size_t file_size, unsigned char *key,
				uint64_t orig_entry)
{
	Elf64_Ehdr		*ehdr;
	Elf64_Phdr		*pt_note;
	Elf64_Phdr		*pt_exec;
	unsigned char	stub[STUB_SIZE];
	uint64_t		stub_vaddr;

	ehdr = (Elf64_Ehdr *)file;

	pt_note = find_pt_note(file);
	if (!pt_note)
		return (write(2, "Error: PT_NOTE segment not found\n", 33), -1);

	pt_exec = find_exec_segment(file);
	if (!pt_exec)
		return (write(2, "Error: No executable PT_LOAD segment\n", 37), -1);

	/*
	** stub_vaddr = dirección virtual DESPUÉS del último PT_LOAD existente.
	** Es critical no colisionar con ningún segmento ya mapeado.
	*/
	stub_vaddr = find_last_load_end(file);

	/*
	** El offset en fichero DEBE estar alineado a página para satisfacer
	** la restricción del kernel ELF loader:
	**   p_vaddr % p_align == p_offset % p_align
	** Como stub_vaddr % 0x1000 == 0, p_offset también debe ser multiplo de 0x1000.
	*/
	size_t stub_offset = (file_size + 0xFFF) & ~(size_t)0xFFF;

	/* Copiar bytecode base y parchear placeholders */
	memcpy(stub, stub_bin, STUB_SIZE);
	patch_stub(stub, pt_exec->p_vaddr, pt_exec->p_filesz, orig_entry, key);

	/*
	** Convertir PT_NOTE en PT_LOAD ejecutable que mapea el stub.
	** p_offset = primera página tras el final del archivo (alineada).
	** p_vaddr  = dirección virtual calculada arriba.
	*/
	pt_note->p_type   = PT_LOAD;
	pt_note->p_flags  = PF_R | PF_X;
	pt_note->p_offset = stub_offset;
	pt_note->p_vaddr  = stub_vaddr;
	pt_note->p_paddr  = stub_vaddr;
	pt_note->p_filesz = STUB_SIZE;
	pt_note->p_memsz  = STUB_SIZE;
	pt_note->p_align  = 0x1000;

	/* Redirigir entry point al stub */
	ehdr->e_entry = stub_vaddr;

	/*
	** Escribir el stub en el buffer: los bytes [file_size .. stub_offset-1]
	** son ceros (padding) y [stub_offset .. stub_offset+STUB_SIZE] es el stub.
	** El buffer fue mapeado con mmap(total_size = stub_offset + STUB_SIZE),
	** con MAP_ANONYMOUS que ya inicializa a ceros, así el padding está listo.
	*/
	memcpy((unsigned char *)file + stub_offset, stub, STUB_SIZE);

	printf("[+] Stub inyectado → offset 0x%lx  vaddr 0x%lx\n",
		stub_offset, stub_vaddr);
	printf("[+] Entry point: 0x%lx → 0x%lx\n", orig_entry, stub_vaddr);
	return (0);
}
