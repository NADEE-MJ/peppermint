<script lang="ts">
	export let userType: 'client' | 'admin' | 'public';
</script>

{#if userType === 'client'}
	<nav class="list-nav p-4">
		<ul>
			<li><a href="/client/accounts">Accounts</a></li>
			<li><a href="/client/transactions">All Transactions</a></li>
			<li><a href="/client/budget/manage">Budget</a></li>
			<li><a href="/client/categories">Categories</a></li>
			<li><a href="/client/budget">Dashboard</a></li>
			<li><a href="/client/filters">Filters</a></li>
		</ul>
	</nav>
{:else if userType === 'admin'}
	<nav class="list-nav p-4">
		<ul>
			<li><a href="/admin/create">Create User / Admin</a></li>
			<li><a href="/admin/manage">Manage Users</a></li>
		</ul>
	</nav>
{/if}
