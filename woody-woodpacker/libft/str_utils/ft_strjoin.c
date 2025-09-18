/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: ncruz-ga <ncruz-ga@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/04/26 18:05:04 by ncruz-ga          #+#    #+#             */
/*   Updated: 2024/10/21 19:48:45 by ncruz-ga         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	size;
	char	*s3;

	size = ft_strlen(s1) + ft_strlen(s2);
	s3 = (char *)malloc(size + 1);
	if (!s3)
		return (0);
	ft_memcpy(s3, s1, ft_strlen(s1));
	ft_memcpy(s3 + ft_strlen(s1), s2, ft_strlen(s2) + 1);
	return (s3);
}
