import '../css/Header.css'

const Header = (props) => {
    return (
        <header className='container'>
            <h1>{props.title}</h1>
        </header>
    )
}

Header.defaultProps = {
    title: 'dafsadsf',
    title2: 'adfad'
}

export default Header
