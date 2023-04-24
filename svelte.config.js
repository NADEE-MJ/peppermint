import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess:	vitePreprocess(),
	kit: {
		files: {
			routes: 'frontend/src/routes',
			appTemplate: 'frontend/src/app.html',
			errorTemplate: 'frontend/src/error.html',
			assets: 'frontend/static',
			hooks: {
				client: 'frontend/src/hooks.client.ts',
				server: 'frontend/src/hooks.server.ts'
			},
			lib: 'frontend/src/lib',
			params: 'frontend/src/params',
			serviceWorker: 'frontend/src/service-worker'
		},
		adapter: adapter(),
		env: {
			dir: '.'
		}
	}
};

export default config;
