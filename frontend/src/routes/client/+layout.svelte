<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../../app.postcss';
	import { AppShell, AppBar, Avatar, Drawer, drawerStore, popup, type PopupSettings, LightSwitch } from '@skeletonlabs/skeleton';
	import Navigation from '$lib/components/Navigation.svelte';

	function drawerOpen(): void {
		drawerStore.open();
	}

	let AccountOptions: PopupSettings = {
		event: 'focus-click',
		target: 'accountOptions',
		placement: 'bottom'
	};
</script>

<Drawer class="w-2/3">
	<Navigation />
</Drawer>

<AppShell slotSidebarLeft="w-0 md:w-52 bg-surface-500/10">
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<button class="md:hidden btn btn-sm mr-4" on:click={drawerOpen}>
					<span>
						<svg viewBox="0 0 100 80" class="fill-token w-4 h-4">
							<rect width="100" height="20" />
							<rect y="30" width="100" height="20" />
							<rect y="60" width="100" height="20" />
						</svg>
					</span>
				</button>
				<strong class="text-3xl uppercase">peppermint</strong>
			</svelte:fragment>

			<svelte:fragment slot="default">
				<div class="grid grid-cols-3">
					<div class="col-start-2 mx-auto">
						<a class="btn btn-md variant-ghost-tertiary w-2/5" href="https://github.com/NADEE-MJ/peppermint">GitHub</a>
						<a class="btn btn-md variant-ghost-tertiary w-2/5" href="https://docs.google.com/document/d/1bKWnTiJezL7QpqsS6EcR1HyTvwvQB3s1RVC6jnCUPJ4"
							>Docs</a
						>
					</div>
				</div>
			</svelte:fragment>

			<svelte:fragment slot="trail">
				<LightSwitch />
				<div>
					<button class="btn" use:popup={AccountOptions}>
						<Avatar src="https://api.dicebear.com/6.x/bottts-neutral/svg?seed=Peppermint" width="w-10" background="bg-primary-500" />
					</button>
					<div class="card w-48 shadow-xl py-2 variant-filled-tertiary" data-popup="accountOptions">
						<nav class="list-nav">
							<ul>
								<li><a href="/client/account">Account</a></li>
							</ul>
						</nav>
						<div class="arrow variant-filled-tertiary" />
					</div>
				</div>

				<form action="/logout" method="POST">
					<button class="btn btn-md variant-filled-secondary">Logout</button>
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
