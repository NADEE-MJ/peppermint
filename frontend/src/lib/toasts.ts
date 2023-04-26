import { toastStore, type ToastSettings } from '@skeletonlabs/skeleton';

const sendToast = (message: string, background: string) => {
	const t: ToastSettings = {
		message: message,
		background: background,
		autohide: true,
		timeout: 5000
	};
	toastStore.trigger(t);
};

export const toast = {
	error: (message: string) => {
		sendToast(message, 'variant-filled-error');
	},
	success: (message: string) => {
		sendToast(message, 'variant-filled-success');
	},
	warning: (message: string) => {
		sendToast(message, 'variant-filled-warning');
	}
};
