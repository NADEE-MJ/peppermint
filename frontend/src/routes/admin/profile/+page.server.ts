import { fail, type Actions, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { fast } from '$lib/fast';
import { UpdateUserValidator } from '$lib/zodValidators';

export const load = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (!token) {
		//! user is not logged in redirect to login
		throw redirect(303, '/login');
	}

	const res = await fast.getCurrentUser(token);
	const user = await res.json();

	if (!user?.id) {
		throw fail(400, { message: 'Invalid Token' });
	}

	return { email: user.email, full_name: user.full_name };
}) satisfies PageServerLoad;

export const actions: Actions = {
	updateUser: async ({ request, cookies }) => {
		const data = Object.fromEntries(await request.formData());

		let password: FormDataEntryValue | null = data.password;
		if (password.length === 0) {
			password = null;
		}

		let passwordConfirm: FormDataEntryValue | null = data.passwordConfirm;
		if (passwordConfirm.length === 0) {
			passwordConfirm = null;
		}

		const dataNullPasswords = {
			email: data.email,
			full_name: data.full_name,
			password,
			passwordConfirm
		};

		const validatedBody = UpdateUserValidator.safeParse(dataNullPasswords);
		if (!validatedBody.success) {
			const { fieldErrors: errors } = validatedBody.error.flatten();
			return fail(400, { errors });
		}
		const body = validatedBody.data;
		const token = cookies.get('access_token');
		if (token) {
			const response = await fast.updateCurrentAdmin(token, body);
			const data = await response.json();

			//! make sure this is working as intended, maybe 500 is not correct code here
			if (response.status != 200) {
				return fail(500, { message: data });
			}

			return { success: true };
		} else {
			return fail(401, { message: 'You are not logged in.' });
		}
	}
};
