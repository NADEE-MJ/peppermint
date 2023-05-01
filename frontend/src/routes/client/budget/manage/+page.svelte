<script lang="ts">
	import { toast } from '$lib/toasts';
	import { modalStore, type ModalSettings } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	let budgetData: { [key: string]: any } = {};
	let noBudget = true;
	let loading = true;
	let rowHeaders = ['name', 'amount'];
	let fullHeaders = ['Name', 'Amount'];

	onMount(async () => {
		await getBudgetData();
	});

	const getBudgetData = async () => {
		let response = await fetch(`/api/budget`, { method: 'GET' });
		let data = await response.json();
		if (data['message']) {
			noBudget = true;
			return;
		}
		noBudget = false;
		budgetData = data['budgets'][0];
	};

	const updateData = async (jsonData: { [key: string]: any }, id: number) => {
		loading = true;

		const response = await fetch('/api/budget', {
			method: 'PUT',
			body: JSON.stringify({ ...jsonData, id }),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await response.json();
		if (data['success']) {
			toast.success('Successfully updated selected row');
			await getBudgetData();
		} else {
			toast.error('Unable to update row');
		}
		loading = false;
	};

	const startEditModal = () => {
		const editModal: ModalSettings = {
			type: 'component',
			component: 'editModal',
			meta: { rowData: budgetData, rowHeaders, fullHeaders, excludeUpdateHeaders: [] },
			title: 'Edit Budget',
			response: (res: { [key: string]: any }) => (res ? updateData(res, budgetData.id) : null)
		};
		modalStore.trigger(editModal);
	};

	const addData = async (jsonData: { [key: string]: any }) => {
		loading = true;

		const response = await fetch('/api/budget', {
			method: 'POST',
			body: JSON.stringify(jsonData),
			headers: { 'Content-Type': 'application/json' }
		});
		const data = await response.json();
		if (data['success']) {
			toast.success('Successfully added budget');
			await getBudgetData();
		} else {
			toast.error('Unable to add budget');
		}
		await getBudgetData();
		noBudget = false;
		loading = false;
	};

	const startCreateModal = () => {
		const createModal: ModalSettings = {
			type: 'component',
			component: 'createModal',
			meta: { rowHeaders, fullHeaders, foreignKeyOptions: null },
			title: 'Create Budget',
			response: (res: { [key: string]: any }) => (res ? addData(res) : null)
		};
		modalStore.trigger(createModal);
	};
</script>

<div class="card p-4 m-auto w-4/5">
	<header class="card-header text-center">
		<strong class="text-5xl">Manage Budget Info</strong>
	</header>

	<div class="p-10">
		{#if !noBudget}
			<div class="grid grid-cols-2 gap-4">
				<div>
					<strong class="text-md">Name</strong>
					<div>{budgetData.name}</div>
				</div>
				<div>
					<strong class="text-md">Amount</strong>
					<div>{budgetData.amount}</div>
				</div>
			</div>
		{/if}

		<div class="grid grid-cols-3 mt-6">
			{#if !noBudget}
				<button class="btn btn-lg variant-filled-primary card-hover col-start-2" on:click={startEditModal}>Edit Budget</button>
			{:else}
				<button class="btn btn-lg variant-filled-primary card-hover col-start-2" on:click={startCreateModal}>Create Budget</button>
			{/if}
		</div>
	</div>
</div>
