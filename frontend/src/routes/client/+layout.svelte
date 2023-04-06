<script lang="ts">
	import '@skeletonlabs/skeleton/themes/theme-crimson.css';
	import '@skeletonlabs/skeleton/styles/all.css';
	import '../../app.postcss';
	import { AppShell, AppBar } from '@skeletonlabs/skeleton';
</script>

<AppShell slotSidebarLeft="bg-surface-500/5 w-56 p-4">
	<svelte:fragment slot="sidebarLeft">
		<nav class="list-nav">
			<ul>
				<li><a href="/client/account">Account</a></li>
				<li><a href="/client/skelly">Skelly</a></li>
			</ul>
		</nav>
	</svelte:fragment>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<strong class="text-xl uppercase">peppermint</strong>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<a class="btn btn-sm btn-ghost-surface" href="https://github.com/NADEE-MJ" target="_blank" rel="noreferrer">GitHub</a>
				<form action="/logout" method="POST">
					<button class="btn btn-filled-secondary btn-sm">Logout</button>
				</form>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>
