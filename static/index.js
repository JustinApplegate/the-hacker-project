async function vote() {
    // change vote button look
    document.getElementById('vote-btn').innerHTML = '<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>';

    // send request
    const response = await fetch('/api/vote');
    const data = await response.json();

    // alert
    if (data.HPD != 0) {
        document.getElementById('alerts').innerHTML = '<div class="alert alert-success alert-dismissible fade show" role="alert">Voting complete.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
    }
    else {
        document.getElementById('alerts').innerHTML = '<div class="alert alert-warning alert-dismissible fade show" role="alert">You already voted for today!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
    }

    // change button back
    document.getElementById('vote-btn').innerHTML = 'Vote';
}

async function sync() {
    // change sync button look
    document.getElementById('sync-btn').innerHTML = '<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>';

    // send request
    const response = await fetch('/api/sync_db');
    const data = await response.json();

    // reload if at /
    if (window.location.pathname == '/') {
        window.location.reload();
    }
}

async function update() {
    // change update button look
    document.getElementById('update-btn').innerHTML = '<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>';

    // send request
    const response = await fetch('/api/update');
    const data = await response.json();

    // reload if at /
    if (window.location.pathname == '/') {
        window.location.reload();
    }
}