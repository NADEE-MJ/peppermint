import { toastStore, type ToastSettings } from '@skeletonlabs/skeleton';

export const toast = {
	error: (message: string) => {
		const t: ToastSettings = {
			message: message,
			preset: 'error',
			autohide: true,
			timeout: 5000
		};
		toastStore.trigger(t);
	}
};
