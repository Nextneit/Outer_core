#include "woody-woodpacker.h"

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

uint64_t	find_encrypted_segment_offset(void *file){
	Elf64_Ehdr	*data;
	Elf64_Phdr	*headers;
	Elf64_Phdr	*segment;
	int			i;

	data = (Elf64_Ehdr *)file;
	headers = (Elf64_Phdr *)((char *)file + data->e_phoff);
	i = 0;
	while (i < data->e_phnum){
		segment = &headers[i];
		if (segment->p_type == PT_LOAD && (segment->p_flags & PF_X))
			return (segment->p_offset);
		i++;
	}
	return (EXIT_FAILURE);
}

size_t	find_encrypted_segment_size(void *file){
	Elf64_Ehdr	*data;
	Elf64_Phdr	*headers;
	Elf64_Phdr	*segment;
	int			i;

	data = (Elf64_Ehdr *)file;
	headers = (Elf64_Phdr *)((char *)file + data->e_phoff);
	i = 0;
	while (i < data->e_phnum){
		segment = &headers[i];
		if (segment->p_type == PT_LOAD && (segment->p_flags & PF_X))
			return (segment->p_filesz);
		i++;
	}
	return (EXIT_FAILURE);
}
