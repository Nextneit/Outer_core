#include "../woody-woodpacker.h"

int	parse_elf64(void *file, size_t size){
	Elf64_Ehdr	*tmp;

	if (!file || size < sizeof(Elf64_Ehdr))
		return (printf("Not ELF file\n"), -1);
	tmp = (Elf64_Ehdr *) file;
	if (tmp->e_ident[0] != ELFMAG0 || tmp->e_ident[1] != ELFMAG1 ||
		tmp->e_ident[2] != ELFMAG2 || tmp->e_ident[3] != ELFMAG3)
		return (printf("Not an ELF file: %02x %02x %02x %02x\n", tmp->e_ident[1], tmp->e_ident[2], tmp->e_ident[2], tmp->e_ident[3]), EXIT_FAILURE);
	if (tmp->e_ident[4] != ELFCLASS64)
		return (printf("File architecture not suported: %d\n", tmp->e_ident[4]), EXIT_FAILURE);
	return (0);
}