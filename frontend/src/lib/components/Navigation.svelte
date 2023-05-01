<script lang="ts">
	export let userType: 'client' | 'admin' | 'public';
</script>

{#if userType === 'client'}
	<nav class="list-nav p-4">
		<ul>
			<li><a href="/client/budget/all">All Transactions</a></li>
			<li><a href="/client/accounts">Accounts</a></li>
			<li><a href="/client/filters">Filters</a></li>
			<li><a href="/client/budget">Budget</a></li>
			<li><a href="/client/categoires">Categories</a></li>
		</ul>
	</nav>
{:else if userType === 'admin'}
	<nav class="list-nav p-4">
		<ul>
			<li><a href="/admin/create">Create User / Admin</a></li>
			<li><a href="/admin/delete">Delete User</a></li>
			<li><a href="/admin/update">Update User</a></li>
			<li><a href="/admin/find">Find User</a></li>
		</ul>
	</nav>
{/if}
