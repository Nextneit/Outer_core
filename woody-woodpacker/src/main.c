#include "../woody-woodpacker.h"

int	main(int argc, char **argv){
	int 		fd;
	size_t		file_size;
	void		*file;

	if (argc != 2)
		return (printf("Usage: ./woody <elf file>\n"), EXIT_FAILURE);
	fd = open(argv[1], O_RDONLY);
	if (fd < 0)
		return (perror("Error opening file"), EXIT_FAILURE);
	file_size = get_file_size(fd);
	if (file_size == 0)
		return (perror("Empty file"), EXIT_FAILURE);
	file = mmap(NULL, file_size, PROT_READ, MAP_PRIVATE, fd, 0);
	if (file == MAP_FAILED)
		return (perror("mmap failed"), close(fd), EXIT_FAILURE);
	if (parse_elf64(file, file_size) != 0){
		printf("Invalid file \n");
		return (munmap(file, file_size), close(fd), EXIT_FAILURE);
	}
	return (0);
}