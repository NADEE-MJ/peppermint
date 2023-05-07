import { fail, redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { fast } from '$lib/fast';

export const load = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (!token) {
		throw redirect(303, '/login');
	}

	const res = await fast.getCurrentUser(token);
	const user = await res.json();

	if (!user?.id) {
		throw fail(400, { message: 'Invalid Token' });
	}

	if (!user?.is_admin) {
		throw redirect(303, '/client/profile');
	}

	return { loggedIn: true };
}) satisfies LayoutServerLoad;
