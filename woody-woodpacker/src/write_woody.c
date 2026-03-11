#include "woody-woodpacker.h"

/*
** write_woody — Escribe el ELF modificado (archivo original + stub) en
** un nuevo fichero llamado "woody" con permisos de ejecución.
**
** El tamaño total = file_size (ELF original) + STUB_SIZE (stub inyectado),
** que coincide exactamente con lo que está en el buffer tras inject_stub().
*/
int	write_woody(void *file, size_t file_size)
{
	int		fd;
	size_t	total_size;

	/* Tamaño total = padding hasta página alineada + stub al final */
	total_size = ((file_size + 0xFFF) & ~(size_t)0xFFF) + STUB_SIZE;
	fd = open("woody", O_WRONLY | O_CREAT | O_TRUNC, 0755);
	if (fd < 0)
		return (perror("Error: cannot create 'woody'"), -1);
	if (write(fd, file, total_size) != (ssize_t)total_size)
		return (perror("Error: write woody"), close(fd), -1);
	close(fd);
	printf("[+] Archivo 'woody' escrito (%zu bytes)\n", total_size);
	return (0);
}
