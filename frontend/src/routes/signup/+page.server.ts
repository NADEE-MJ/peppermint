import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { signupValidator, loginValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';

export const actions: Actions = {
	signup: async ({ request, cookies }) => {
		const body = Object.fromEntries(await request.formData());

		const validatedBody = signupValidator.safeParse(body);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			return fail(400, { errors });
		}
		const { email, password, full_name } = validatedBody.data;

		const res = await fast.signup( email, password, full_name);
		const data = await res.json();

		if (data?.full_name) {

			const temp = await fast.login(email, password);
			const datata = await res.json();

			if (datata?.access_token) {
				const token = datata?.access_token;
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
				return fail(400, { error: 'Very Wrong' });
			}

		}

		else {
			return fail(400, {error: "Wrong"});
		}
	}
};
