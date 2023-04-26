import { localStorageStore } from '@skeletonlabs/skeleton';
import type { Writable } from 'svelte/store';

export type User = {
	id: number;
	full_name: string;
	email: string;
} | null;

export const userStore: Writable<User> = localStorageStore('user', null);
