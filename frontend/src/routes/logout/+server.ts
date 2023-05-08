import { fast } from '$lib/fast';
import { redirect, type RequestHandler } from '@sveltejs/kit';

export const POST = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	cookies.delete('access_token');

	if (!token) {
		throw redirect(303, '/');
	}

	const res = await fast.logout(token);
	const data = await res.json();
	if (res.status !== 200 && data?.success !== true) {
		throw new Error('Failed to logout');
	}

	throw redirect(303, '/');
}) satisfies RequestHandler;
