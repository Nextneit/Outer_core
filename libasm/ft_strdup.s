section .text
global ft_strdup
extern malloc
extern ft_strlen
extern ft_strcpy

ft_strdup:
	;Check if src = NULL
	test rdi, rdi
	jz	.null

	;save src get lenght and add null
	push rdi
	call ft_strlen
	inc rax

	;size of malloc and allocate
	mov rdi, rax
	call malloc wrt ..plt

	;chech malloc = NULL
	test rax, rax
	jz .malloc_failed

	;dst = malloc src = original string and copy
	mov rdi, rax
	mov rsi, [rsp]
	call ft_strcpy

	;clean stack and ret *
	add rsp, 8
	ret

.malloc_failed:
	;clean stack a ret NULL
	add rsp, 8
	xor rax, rax
	ret

.null:
	;ret NULL if src = NULL
	xor rax, rax
	ret