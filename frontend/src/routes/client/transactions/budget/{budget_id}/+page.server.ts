import { fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { UpdateUserValidator } from '$lib/zodValidators';
import { fast } from '$lib/fast';
import { userStore } from '$lib/stores';
import { get } from 'svelte/store';

export const load = (async ({cookies}) => {
	const token = cookies.get('access_token');
	const user = get(userStore);
	if (token && user) {
		const response = await fast.getTransactionsByBudget(token, data.budgetId, data.page);
		const jsonData = await response.json();

		return jsonData;
	} else {

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
			const data = await response.json();

			//! make sure this is working as intended, maybe 500 is not correct code here
			if (response.status != 200) {
				return fail(500, { message: data });
			}

			userStore.set({ id: data.id, full_name: data.full_name, email: data.email });

			return { success: true };
		} else {
			return fail(401, { message: 'You are not logged in.' });
		}
	},
    getTransactionsByBudget: async ({ request, cookies }) => {
		const data = Object.fromEntries(await request.formData());
		const token = cookies.get('access_token');
		if (token) {
			const response = await fast.getTransactionsByBudget(token, data.budgetId, data.page);
			const jsonData = await response.json();

			return jsonData;
		} else {

		}
	}
};
