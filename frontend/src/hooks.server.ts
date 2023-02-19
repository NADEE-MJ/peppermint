import { redirect, type Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('access_token')

	if (event.url.pathname.startsWith('/login') && token) {
		throw redirect(303, '/admin/account');
	}

	if (event.url.pathname.startsWith('/client') || event.url.pathname.startsWith('/admin')) {
		// protect client and admin routes
		//! here should probably hit test-access-token route to ensure that the token is valid
		if (!token) {
			console.log('Please log in to access client and admin routes');
			throw redirect(303, '/login');
		}
	}

	return resolve(event);
};
