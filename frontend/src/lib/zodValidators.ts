import { z } from 'zod';

export const loginValidator = z.object({
	email: z.string({ required_error: 'Email is required.' }).min(1, 'Email is required.').email({ message: 'Please provide a valid email.' }),
	password: z.string({ required_error: 'Password is required.' }).min(1, 'Password is required.')
});

export const signupValidator = z
	.object({
		email: z.string().email({ message: 'Please provide a valid email.' }),
		password: z.string().min(8, 'Password must be at least 8 characters.').max(32, 'Password must be less than 32 characters.'),
		passwordConfirm: z.string().min(8, 'Password must be at least 8 characters.').max(32, 'Password must be less than 32 characters.'),
		full_name: z.string().min(1, 'Full Name must be at least 1 character')
	})
	.superRefine(({ password, passwordConfirm }, ctx) => {
		if (password !== passwordConfirm) {
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['password']
			});
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['passwordConfirm']
			});
		}
	});

export const UpdateUserValidator = z
	.object({
		email: z.nullable(z.string().email({ message: 'Please provide a valid email.' })),
		password: z.nullable(z.string().min(8, 'Password must be at least 8 characters.').max(32, 'Password must be less than 32 characters.')),
		passwordConfirm: z.nullable(z.string().min(8, 'Password must be at least 8 characters.').max(32, 'Password must be less than 32 characters.')),
		full_name: z.nullable(z.string().min(1, 'Full Name must be at least 1 character'))
	})
	.superRefine(({ password, passwordConfirm }, ctx) => {
		if (password !== passwordConfirm) {
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['password']
			});
			ctx.addIssue({
				code: 'custom',
				message: 'Password and Confirm Password must match',
				path: ['passwordConfirm']
			});
		}
	});
