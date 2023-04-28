import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { userStore } from '$lib/stores';
import { get } from 'svelte/store';

export const load = (async () => {
	const user = get(userStore);
	if (user) {
		return { email: user.email, full_name: user.full_name };
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies LayoutServerLoad;
