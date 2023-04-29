import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { createUserOrAdminValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';

export const actions: Actions = {
	createUserOrAdmin: async ({ request, cookies }) => {
		const body = Object.fromEntries(await request.formData());

		const validatedBody = createUserOrAdminValidator.safeParse(body);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			return fail(400, { errors });
		}
		const { admin, email, password, full_name } = validatedBody.data;

		const res = await fast.createUserOrAdmin(admin, email, password, full_name);
		let data = await res.json();

        if (data?.full_name) {
			const temp = await fast.login(email, password);
			data = await temp.json();

			if (data?.access_token) {
				const token = data?.access_token;
				cookies.set('access_token', token, {
					path: '/',
					httpOnly: true,
					sameSite: false,
					secure: true,
					maxAge: 60 * 60 * 24 * 30 //30 days //!probably should change this
				});

			} else {
				//! return value from backend
				return fail(400, { error: 'Unable to create new user!' });
			} 
		} else {
			return fail(400, { error: 'Unable to create new user' });
		}
	}
};