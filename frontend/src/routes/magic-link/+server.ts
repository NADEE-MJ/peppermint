import { error, json, redirect, type RequestHandler } from '@sveltejs/kit';
import { fast } from '$lib/fast';

export const GET = (async ({ url, cookies }) => {
	const token = url.searchParams.get('token');

	if (token) {
		const res = await fast.magicLink(token);
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

			if (data?.is_admin) {
				throw redirect(303, '/admin/profile');
			}
			throw redirect(303, '/client/profile');
		} else {
			throw error(400, 'Invalid Token');
		}
	} else {
		throw error(400, 'No token provided');
	}
}) satisfies RequestHandler;

export const POST = (async ({ url }) => {
	const email = url.searchParams.get('email');

	if (email !== 'false' && email) {
		const res = await fast.sendMagicLink(email);
		const data = await res.json();

		if (data?.success) {
			return json({ success: true });
		} else {
			throw error(400, 'Invalid Email');
		}
	} else {
		throw error(400, 'No email provided');
	}
}) satisfies RequestHandler;
