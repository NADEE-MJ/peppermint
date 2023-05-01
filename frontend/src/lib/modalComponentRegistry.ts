import type { ModalComponent } from '@skeletonlabs/skeleton';
import EditModal from '$lib/components/EditModal.svelte';
import CreateModal from '$lib/components/CreateModal.svelte';
import UploadModal from '$lib/components/UploadModal.svelte';

export const modalComponentRegistry: Record<string, ModalComponent> = {
	editModal: { ref: EditModal },
	createModal: { ref: CreateModal },
	uploadModal: { ref: UploadModal }
};
