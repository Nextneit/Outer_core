#include "../woody-woodpacker.h"

size_t	get_file_size(int fd){
	off_t	current;
	off_t	size;

	current = lseek(fd, 0, SEEK_CUR);
	if (current == -1)
		return (perror("lseek"), (size_t) -1);
	size = lseek(fd, 0, SEEK_END);
	if (size == -1)
		return (perror("lseek"), (size_t) -1);
	if (lseek(fd, current, SEEK_SET) == -1)
		return (perror("lseek"), (size_t) -1);
	printf("size = %zu\n", (size_t) size);
	return ((size_t) size);
}

int	print_magic_number(void *file, size_t size){
	Elf64_Ehdr *tmp;
	
	if (!file || size < sizeof(Elf64_Ehdr))
		return (printf("Not ELF file\n"), EXIT_FAILURE);
	tmp = (Elf64_Ehdr *)file;
	printf("ELF file: %02x %02x %02x %02x\n", tmp->e_ident[1], tmp->e_ident[2], tmp->e_ident[2], tmp->e_ident[3]);
	return (0);
}

void	print_key(unsigned char *key, size_t len){
	size_t	i;
	
	i = 0;
	printf("key = ");
	while (i < len){
		printf("%02X", key[i]);
		i++;
	}
	printf("\n");
}
