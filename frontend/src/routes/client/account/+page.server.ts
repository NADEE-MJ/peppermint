import { fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { UpdateUserValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';

export const load = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getCurrentUser(token);
		const json = await response.json();

		return {
			userRecord: json,
			id: json.id
		};
	} else {
		//! let user know they are not logged in
	}
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
			const response = await fast.updateCurrentUser(token, body);
			const message = await response.json();

			//! make sure this is working as intended, maybe 500 is not correct code here
			if (response.status != 200) {
				return fail(500, { message: message });
			}

			return { success: true };
		} else {
			return fail(401, { message: 'You are not logged in.' });
		}
	}
};
