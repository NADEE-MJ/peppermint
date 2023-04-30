import { fast } from '$lib/fast';
import { redirect, type RequestHandler, json } from '@sveltejs/kit';

export const GET = (async ({ cookies }) => {
	const token = cookies.get('access_token');
	if (token) {
		const response = await fast.getAllCategoriesForUser(token);
		const data = await response.json();
		if (data.length === 0) {
			throw new Error('No categories found');
		}

		return json({ categories: data });
	} else {
		//! user is not logged in
		throw redirect(303, '/login');
	}
}) satisfies RequestHandler;
