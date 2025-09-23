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