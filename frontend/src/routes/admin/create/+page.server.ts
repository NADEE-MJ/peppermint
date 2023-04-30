import { fail } from '@sveltejs/kit';
import type { Actions } from './$types';
import { createUserOrAdminValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';

export const actions: Actions = {
	createUserOrAdmin: async ({ request, cookies }) => {
		const token = cookies.get('access_token');
		if (token) {
			const body = Object.fromEntries(await request.formData());
			const isAdminString = body.isAdmin;
			if (isAdminString !== 'true' && isAdminString !== 'false') {
				return fail(400, { error: 'isAdmin must be true or false' });
			}

			const validatedBody = createUserOrAdminValidator.safeParse({ ...body, isAdmin: isAdminString === 'true' });
			if (!validatedBody.success) {
				const { fieldErrors: errors } = validatedBody.error.flatten();
				return fail(400, { errors });
			}
			const { isAdmin, email, password, full_name } = validatedBody.data;

			const res = await fast.createUserOrAdmin(token, { email, password, full_name, isAdmin });
			const data = await res.json();
			if (data?.full_name) {
				return data;
			} else {
				//! return value from backend
				return fail(400, { error: 'Unable to create new user!' });
			}
		} else {
			return fail(400, { error: 'You are not logged in' });
		}
	}
};
