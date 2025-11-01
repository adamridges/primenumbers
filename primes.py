import click


def is_prime(n):
    """Check if a number is prime."""
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_first_primes(count):
    """Get the first 'count' prime numbers."""
    if not isinstance(count, int):
        raise TypeError("Count must be an integer")
        
    # Edge Case: Handle negative or zero count
    if count <= 0:
        return []
    
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


def get_nth_prime(n):
    """Get the nth prime number (1-indexed)."""
    if not isinstance(n, int):
        raise TypeError("N must be an integer")
        
    # Edge Case: Handle invalid nth value (negative or zero)
    if n <= 0:
        return None
    
    primes = get_first_primes(n)
    return primes[-1] if primes else None


@click.group()
def cli():
    """Prime number CLI application."""
    pass


@cli.command(name='get-first-primes')
@click.argument('count', type=int)
def get_first_primes_cmd(count):
    """Get the first COUNT prime numbers."""
    # Edge Case: Handle negative count
    if count < 0:
        click.echo("Count must be a non-negative integer.")
        return
    
    try:
        primes = get_first_primes(count)
        if primes:
            click.echo(" ".join(map(str, primes)))
        else:
            # Edge Case: Handle zero count
            click.echo("")
    except Exception as e:
        click.echo(f"Error: {e}")


@cli.command(name='get-nth-prime')
@click.argument('n', type=int)
def get_nth_prime_cmd(n):
    """Get the Nth prime number."""
    # Edge Case: Handle invalid nth value (negative or zero)
    if n <= 0:
        click.echo("N must be a positive integer.")
        return
    
    try:
        prime = get_nth_prime(n)
        if prime is not None:
            click.echo(prime)
        else:
            # Edge Case: Handle case when no prime is found (shouldn't happen with valid input)
            click.echo("")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()