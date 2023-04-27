import { fast } from '$lib/fast';
import { redirect, type RequestHandler } from '@sveltejs/kit';
// import { fast } from '$lib/fast'; //! create a method in fast to logout on backend as well
import { userStore } from '$lib/stores';

export const POST: RequestHandler = async ({ cookies }) => {
	cookies.delete('access_token');
	userStore.set(null);

	//! need to add token to token blocklist on backend so it cannot be used again

	throw redirect(303, '/');
};
