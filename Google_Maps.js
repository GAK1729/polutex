// import React, { Component } from 'react';
import GoogleMapReact from 'google-map-react';
// import PropTypes from 'prop-types';

const AnyReactComponent = ({ text }) => <div>{text}</div>;
const defaultOptions = {
    radius: 100,
    opacity: 0.6
};

export default class SimpleMap extends Component {
    constructor(props) {
        super(props);
        this.state = {
            center: {
                lat: 1.3521,
                lng: 103.8198
            },
            mapData: {
                positions: [
                    {lat: 0, lng: 0, weight: 0},
                ],
                options: defaultOptions
            },
            zoom: 11.4
        };
        this.onMap = this.onMap.bind(this);
    }

    onMap(data){
        this.setState({
            mapData: {
                positions: data,
                options: defaultOptions
            }
        });
    }
    render() {
        return (
            // Important! Always set the container height explicitly
            <div style={{ height: '50vh', width: '100%' }}>
                <GoogleMapReact
                    bootstrapURLKeys={{ key: 'AIzaSyCi_Io_PnIis5JMPqHK-miIR5BZnqtxMMI' }}
                    defaultCenter={this.state.center}
                    defaultZoom={this.state.zoom}
                    heatmapLibrary={true}
                    heatmap={this.state.mapData}
                >
                    <AnyReactComponent
                        lat={this.state.center.lat}
                        lng={this.state.center.lng}
                        text="Center of Singapore"
                    />
                </GoogleMapReact>
            </div>
        );
    }
}

AnyReactComponent.PropTypes = {
    text: PropTypes.string
}
