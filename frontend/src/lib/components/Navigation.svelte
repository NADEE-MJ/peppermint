<script lang="ts">
	import { drawerStore } from '@skeletonlabs/skeleton';

	function drawerClose(): void {
		drawerStore.close();
	}
</script>

<nav class="list-nav p-4">
	<ul>
		<li><a href="/client/skelly" on:click={drawerClose}>Skelly</a></li>
		<li><a href="/client/transactions/budget/1" on:click={drawerClose}>transactions</a></li>
	</ul>
</nav>
