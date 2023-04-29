<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../app.postcss';
	import { storePopup, Toast, Modal, AppShell, AppBar } from '@skeletonlabs/skeleton';
	import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
	import Navigation from '$lib/components/Navigation.svelte';
	import AccountOptions from '$lib/components/AccountOptions.svelte';
	import ImportantLinks from '$lib/components/ImportantLinks.svelte';
	import { page } from '$app/stores';
	import { modalComponentRegistry } from '$lib/modalComponentRegistry';

	storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

	$: isAdminPage = $page.url.pathname.includes('/admin');
	$: isClientPage = $page.url.pathname.includes('/client');

	const backgroundColor = () => {
		if (isAdminPage) {
			return 'bg-blue-500/30';
		} else if (isClientPage) {
			return 'bg-red-500/30';
		} else {
			return 'bg-gray-500/30';
		}
	};

	const getType = () => {
		if (isAdminPage) {
			return 'admin';
		} else if (isClientPage) {
			return 'client';
		} else {
			return 'public';
		}
	};
</script>

<svelte:head>
	<title>Peppermint</title>
	<meta name="description" content="Peppermint Finance Tracker" />
</svelte:head>

<!-- singletons must be imported in the root layout -->
<Modal components={modalComponentRegistry}/>
<Toast position="bl" max={5} />

{#if isAdminPage || isClientPage}
	<AppShell slotSidebarLeft="w-52 bg-surface-500/10">
		<svelte:fragment slot="header">
			<AppBar background={backgroundColor()}>
				<svelte:fragment slot="lead">
					<strong class="text-3xl uppercase">peppermint</strong>
				</svelte:fragment>

				<svelte:fragment slot="default">
					<ImportantLinks />
				</svelte:fragment>

				<svelte:fragment slot="trail">
					{#if isAdminPage}
						<strong class="text-3xl uppercase">ADMIN</strong>
					{/if}
					<AccountOptions userType={getType()} />
				</svelte:fragment>
			</AppBar>
		</svelte:fragment>

		<svelte:fragment slot="sidebarLeft">
			<Navigation userType={getType()} />
		</svelte:fragment>

		<div class="container p-10 mx-auto">
			<slot />
		</div>
	</AppShell>
{:else}
	<slot />
{/if}
