#ifndef WOODY_WOODPACKER
# define WOODY_WOODPACKER

	#include <stdio.h>
	#include <stdlib.h>
	#include <stdint.h>			// Tipos enteros específicos (uint64_t, etc.)
	#include <string.h>
	#include <sys/mman.h>		// mmap, munmap, mprotect
	#include <fcntl.h>
	#include <unistd.h>
	#include <time.h>			// Para generar claves aleatorias
	#include <sys/syscall.h>	// Syscalls directas

	// Utils define
	#define	KEY_SIZE 16

	// Constantes ELF
	#define EI_NIDENT 16	//Tamaño del array
	#define ELFMAG0 0x7f	//Primer byte
	#define ELFMAG1 'E'		//Segundo byte
	#define ELFMAG2 'L'		//Tercer byte
	#define ELFMAG3 'F'		//Cuarto byte
	#define ELFCLASS64 2	//Arquitectura 64-bit
	#define ELFDATA2LSB 1	//Little-endian

	#define ET_EXEC 2		//Ejecutable
	#define ET_DYN  3		//Shared object/PIE

	#define PT_LOAD    1	//Segmento cargable en memoria
	#define PF_X 1 			//Ejecutable
	#define PF_W 2  		//Escribible
	#define PF_R 4  		//Legible

	// Estructuras ELF64
	typedef struct {
		unsigned char e_ident[EI_NIDENT]; 	// [0x7f,'E','L','F', class, data, version...]
		uint16_t e_type;          			// Tipo: ET_EXEC, ET_DYN...
		uint16_t e_machine;       			// Arquitectura: x86_64 = 0x3E
		uint32_t e_version;       			// Versión ELF
		uint64_t e_entry;         			// ⭐ PUNTO DE ENTRADA (donde modificas)
		uint64_t e_phoff;         			// Offset a program headers
		uint64_t e_shoff;         			// Offset a section headers
		uint32_t e_flags;         			// Flags específicas del procesador
		uint16_t e_ehsize;        			// Tamaño de este header
		uint16_t e_phentsize;     			// Tamaño de cada program header
		uint16_t e_phnum;         			// Número de program headers
		uint16_t e_shentsize;     			// Tamaño de cada section header
		uint16_t e_shnum;         			// Número de section headers
		uint16_t e_shstrndx;      			// Índice de string table
	} Elf64_Ehdr;

	typedef struct {
		uint32_t p_type;     // Tipo: PT_LOAD, PT_DYNAMIC...
		uint32_t p_flags;    // Permisos: PF_R|PF_W|PF_X
		uint64_t p_offset;   // Offset en el archivo
		uint64_t p_vaddr;    // ⭐ Dirección virtual donde cargar
		uint64_t p_paddr;    // Dirección física (igual que vaddr)
		uint64_t p_filesz;   // ⭐ Tamaño en archivo
		uint64_t p_memsz;    // ⭐ Tamaño en memoria
		uint64_t p_align;    // Alineación requerida
	} Elf64_Phdr;

	typedef struct {
		uint32_t sh_name;      // Offset al nombre en string table
		uint32_t sh_type;      // Tipo de sección
		uint64_t sh_flags;     // Flags (escribible, ejecutable...)
		uint64_t sh_addr;      // Dirección virtual
		uint64_t sh_offset;    // Offset en archivo
		uint64_t sh_size;      // Tamaño de la sección
		uint32_t sh_link;      // Link a otra sección
		uint32_t sh_info;      // Info adicional
		uint64_t sh_addralign; // Alineación
		uint64_t sh_entsize;   // Tamaño de entradas (si es tabla)
	} Elf64_Shdr;

	// ✅ SOLO DECLARACIONES (extern) - NO DEFINICIONES
    extern unsigned char decryption_stub[];
    extern size_t decryption_stub_size;
    extern unsigned char woody_message[];
    extern size_t woody_message_size;

	//Utils
	size_t	get_file_size(int fd);
	int		print_magic_number(void *file, size_t size);
	void	print_key(unsigned char *key, size_t len);

	//Crypto
	void	generate_random_key(unsigned char* key, size_t len);
	int		encrypt_segment(void *file, size_t size, unsigned char *key);
	void 	xor_encrypt(unsigned char *data, size_t len, unsigned char *key, size_t key_len);

	//Parse
	int		parse_elf64(void *file, size_t size);

#endif