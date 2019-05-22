class popNomMarker extends React.Component {
    render() {
        return (
            <div className="marker">
                <h2>Name: {this.props.name}</h2>
                <img src={this.props.imgUrl} />
                <h2>Skill: </h2>
            </div>
        );
    }
}

ReactDOM.render(
    <popNomMarker name="Balloonicorn" skill="video games" imgUrl="/static/img/balloonicorn.jpg" />, 
    document.getElementById('balloonicorn') 
);