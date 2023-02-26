function eventCheckBox() {
    const cardsToApprove = Array.from(document.getElementsByClassName("approval-card"));
    cardsToApprove.forEach((item) => item.checked = !item.checked);
}

function addFilter(field) {
    return `<a href="#" class="filter-icon filter-apply" title="Применить фильтр" data-field="${field}" onclick="applyFilters(this.getAttribute('data-field'))" >
                            <img src="/static/img/apply-icon-gray.png" width="20px" alt="" />
                          </a>`;
}

function drawFilterOptions() {
    const filterItems = Array.from(document.getElementsByClassName("filter-list"));
    const cancelButton = `<a href="#" class="filter-icon filter-reset" title="Сбросить все фильтры" onclick="resetFilters(event)">
                            <img src="/static/img/cancel-icon-gray.png" width="20px" alt="" />
                          </a>`;
    filterItems.forEach((item) => item.innerHTML += addFilter(item.querySelector('input, select').name) + cancelButton);
}

function applyFilters(field) {
    const filterValue = document.getElementById('id_' + field).value;
    if (filterValue) {
      window.location.href = `?${field}=${filterValue}`;
    }
}

function resetFilters(event) {
    event.preventDefault();
    window.location.href = '?reset';
}

drawFilterOptions();
