#include "../woody-woodpacker.h"

void	generate_random_key(unsigned char* key, size_t len){
	int		fd;
	size_t	i;

	i = 0;
	fd = open("/dev/random", O_RDONLY);
	if (fd < 0){
		srand(time(NULL));
		while(i < len){
			key[i] = rand() % 256;
			i++;
		}
	}
	else{
		read(fd, key, len);
		close(fd);
	}
}

int	encrypt_segment(void *file, size_t size, unsigned char *key){
	Elf64_Ehdr	*data;
	Elf64_Phdr	*headers;
	int			i;
	size_t		j;

	data = (Elf64_Ehdr *) file;
	headers = (Elf64_Phdr *)((char *)file + data->e_phoff);
	i = 0;
	j = 0;
	while (i < data->e_phnum){
		Elf64_Phdr *segment;
		segment = &headers[i];
		if (segment->p_offset + segment->p_filesz > size)
			return (printf("Segment outside file bounds\n"), -1);
		if (segment->p_type == PT_LOAD && (segment->p_flags & PF_X)){
			unsigned char *segment_data;
			segment_data = (unsigned char *)file + segment->p_offset;
			printf("Segment offset: 0x%lx\n", segment->p_offset);
			printf("Segment size: %zu\n", segment->p_filesz);
			printf("File size: %zu\n", size);
			printf("Original bytes: ");
			while(j < 16 && j < segment->p_filesz){
				printf("%02x ", segment_data[j]);
				j++;
			}
			printf("\n");
			xor_encrypt(segment_data, segment->p_filesz, key, KEY_SIZE);
			j = 0;
			printf("Encrypted bytes: ");
			while(j < 16 && j < segment->p_filesz){
				printf("%02x ", segment_data[j]);
				j++;
			}
			printf("\n");
			printf("Segment encrypted: offset=0x%lx, size=%zu\n", segment->p_offset, segment->p_filesz);
			return (EXIT_SUCCESS);
		}
		i++;
	}
	return (printf("No executable segment found\n"), -1);
}

void xor_encrypt(unsigned char *data, size_t len, unsigned char *key, size_t key_len) {
    size_t	i;

	i = 0;
	while(i < len){
        data[i] ^= key[i % key_len];
		i++;
    }
}

int	create_woody_file(void *original_file, size_t size, unsigned)