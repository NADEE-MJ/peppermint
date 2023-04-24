<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../../app.postcss';
	import { AppShell, AppBar, Avatar, Drawer, drawerStore } from '@skeletonlabs/skeleton';
	import Navigation from '$lib/components/navigation.svelte';

	function drawerOpen(): void {
		drawerStore.open();
	}
</script>

<Drawer>
	<Navigation />
</Drawer>

<AppShell slotSidebarLeft="w-0 md:w-52 bg-surface-500/10">
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<button class="md:hidden btn btn-sm mr-4" on:click={drawerOpen}>
					<span>
						<svg viewBox="0 0 100 80" class="fill-token w-4 h-4">
							<rect width="100" height="20"/>
							<rect y="30" width="100" height="20"/>
							<rect y="60" width="100" height="20"/>
						</svg>
					</span>
				</button>
				<strong class="text-xl uppercase">peppermint</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<a class="btn btn-md variant-ghost-surface" href="https://github.com/NADEE-MJ/peppermint" target="_blank" rel="noreferrer">GitHub</a>
				<Avatar initials="PM" width="w-10" background="bg-primary-500" />
				<form action="/logout" method="POST">
					<button class="btn variant-filled-secondary btn-md">Logout</button>
				</form>
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
