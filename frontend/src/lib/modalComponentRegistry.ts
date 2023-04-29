import type { ModalComponent } from '@skeletonlabs/skeleton';
import EditModal from '$lib/components/EditModal.svelte';
import CreateModal from '$lib/components/CreateModal.svelte';

export const modalComponentRegistry: Record<string, ModalComponent> = {
	editModal: {
		ref: EditModal,
		// Add the component properties as key/value pairs
		props: { background: 'bg-red-500' },
		// Provide a template literal for the default component slot
		slot: '<p>Skeleton</p>'
	},

	createModal: {
		ref: CreateModal,
		// Add the component properties as key/value pairs
		props: { background: 'bg-red-500' },
		// Provide a template literal for the default component slot
		slot: '<p>Skeleton</p>'
	}
};
