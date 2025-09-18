/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/04/20 15:04:12 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:48:56 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	unsigned int	count;

	count = 0;
	while ((s1[count] != '\0' || s2[count] != '\0') && (count < n))
	{
		if ((unsigned char)s1[count] < (unsigned char)s2[count])
			return (-1);
		if ((unsigned char)s1[count] > (unsigned char)s2[count])
			return (1);
		count++;
	}
	return (0);
}
