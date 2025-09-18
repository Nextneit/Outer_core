section .text
global	ft_strcpy

ft_strcpy:
	;check if src is NULL
	test rsi, rsi
	jz .done
	;initialize index counter
	xor rcx, rcx

.copy:
	;load byte from src and store in dst
	mov dl, BYTE [rsi + rcx]
	mov BYTE [rdi + rcx], dl
	;increment index
	inc rcx
	;check if byte was null terminator
	test dl, dl
	jne .copy

.done:
	;return pointer to dst
	mov rax, rdi
	ret