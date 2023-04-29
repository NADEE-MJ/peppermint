<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import Navigation from '$lib/components/ClientNavigation.svelte';
	import ClientAccountOptions from '$lib/components/ClientAccountOptions.svelte';
	import ImportantLinks from '$lib/components/ImportantLinks.svelte';
</script>

<AppShell slotSidebarLeft="w-52 bg-surface-500/10">
	<svelte:fragment slot="header">
		<AppBar background="bg-red-500/30">
			<svelte:fragment slot="lead">
				<strong class="text-3xl uppercase">peppermint</strong>
			</svelte:fragment>

			<svelte:fragment slot="default">
				<ImportantLinks />
			</svelte:fragment>

			<svelte:fragment slot="trail">
				<ClientAccountOptions />
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>

	<svelte:fragment slot="sidebarLeft">
		<Navigation />
	</svelte:fragment>

	<div class="container p-10 mx-auto">
		<slot />
	</div>
</AppShell>
