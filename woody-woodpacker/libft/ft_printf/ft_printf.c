/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/07/20 10:27:59 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:15:34 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_filter(char const *content, int i, va_list *args)
{
	int	print_count;

	print_count = 0;
	if (content[i] == 'c')
		print_count = ft_putchar(va_arg(*args, int));
	if (content[i] == 's')
		print_count = ft_printstr(va_arg(*args, char *));
	if (content[i] == 'p')
		print_count = ft_printptr(va_arg(*args, unsigned long long));
	if (content[i] == 'd' || content[i] == 'i')
		print_count = ft_printdec(va_arg(*args, int));
	if (content[i] == 'u')
		print_count = ft_printunsigned(va_arg(*args, unsigned int));
	if (content[i] == 'x' || content[i] == 'X')
		print_count = ft_printhexa(va_arg(*args, unsigned int), content[i]);
	if (content[i] == '%')
		print_count = ft_putchar('%');
	return (print_count);
}

int	ft_printf(char const *content, ...)
{
	va_list	args;
	int		i;
	int		c;

	i = 0;
	c = 0;
	va_start(args, content);
	while (content[i])
	{
		if (content[i] == '%')
		{
			i++;
			c += ft_filter(content, i, &args);
		}
		else
			c += ft_putchar(content[i]);
		if (c == -1)
			return (-1);
		i++;
	}
	return (va_end(args), c);
}
