import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { loginValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';

export const actions: Actions = {
	login: async ({ request, cookies }) => {
		const body = Object.fromEntries(await request.formData());

		const validatedBody = loginValidator.safeParse(body);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			return fail(400, { errors });
		}
		const { email, password } = validatedBody.data;

		const res = await fast.login(email, password);
		const data = await res.json();
		if (data?.access_token) {
			const token = data?.access_token;
			cookies.set('access_token', token, {
				path: '/',
				httpOnly: true,
				sameSite: false,
				secure: true,
				maxAge: 60 * 60 * 24 * 30 //30 days //!probably should change this
			});

			throw redirect(303, '/client/account');
		} else {
			//! return value from backend
			return fail(400, { error: 'Invalid Credentials' });
		}
	}
};
