import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { loginValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';
import { userStore } from '$lib/stores';
import { get } from 'svelte/store';

export const load = (async () => {
	const user = get(userStore);
	if (user) {
		throw redirect(303, '/client/account');
	}
}) satisfies PageServerLoad;

export const actions: Actions = {
	login: async ({ request, cookies }) => {
		const body = Object.fromEntries(await request.formData());

		const validatedBody = loginValidator.safeParse(body);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			return fail(400, { errors });
		}
		const { email, password } = validatedBody.data;

		let res = await fast.login(email, password);
		const data = await res.json();
		if (data?.access_token) {
			const token = data?.access_token;
			cookies.set('access_token', token, {
				path: '/',
				httpOnly: true,
				sameSite: true,
				secure: false,
				maxAge: 60 * 60 * 24 * 30 //30 days //!probably should change this
			});

			res = await fast.getCurrentUser(token);
			const user = await res.json();
			userStore.set({ id: user.id, full_name: user.full_name, email: user.email });

			throw redirect(303, '/client/account');
		} else {
			//! return value from backend
			return fail(400, { error: 'Invalid Credentials' });
		}
	}
};
