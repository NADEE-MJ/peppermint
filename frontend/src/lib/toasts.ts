import { toastStore, type ToastSettings } from '@skeletonlabs/skeleton';

export const toast = {
	error: (message: string) => {
		const t: ToastSettings = {
			message: message,
			background: 'variant-filled-warning',
			autohide: true,
			timeout: 5000
		};
		toastStore.trigger(t);
	}
};
