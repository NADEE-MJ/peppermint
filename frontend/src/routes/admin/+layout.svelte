<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
	import Navigation from '$lib/components/AdminNavigation.svelte';
	import AdminAccountOptions from '$lib/components/AdminAccountOptions.svelte';
	import ImportantLinks from '$lib/components/ImportantLinks.svelte';


</script>

<AppShell slotSidebarLeft="w-52 bg-surface-500/10">
	<svelte:fragment slot="header">
		<AppBar background='bg-blue-500/30'>
			<svelte:fragment slot="lead">
				<strong class="text-3xl uppercase">peppermint</strong>
			</svelte:fragment>

			<svelte:fragment slot="default">
                <ImportantLinks/>
			</svelte:fragment>

			<svelte:fragment slot="trail">
				<strong class="text-3xl uppercase">ADMIN</strong>
                <AdminAccountOptions/>
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
