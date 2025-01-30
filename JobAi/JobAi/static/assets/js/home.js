function select(element)
{
    document.querySelectorAll('.option').forEach(opt=>opt.classList.remove('select'));
    element.classList.add('select');

}