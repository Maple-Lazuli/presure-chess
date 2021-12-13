import React from 'react';
// import unsplash from '../api/unsplash'
import Board from './Board';
import 'semantic-ui-css/semantic.min.css'
class App extends React.Component {
    state = {
        message1: '',
        message2: '',
        message3: '',
        message4: '',
        white_move: "",
        white_distro: "",
        white_move_ml: "",
        white_distro_ml: "",
        black_move: "",
        black_distro: "",
        black_move_ml: "",
        black_distro_ml: ""
    }

    updateMessage = (text) => {
        this.setState({
            message1: this.state.message2,
        }, () => {
            this.setState({
                message2: this.state.message3
            }, () => {
                this.setState({
                    message3: this.state.message4
                }, () => {
                    this.setState({ message4: text })
                })
            })
        })
    }

    updateMoves = (moveData) => {
        this.setState({
            white_move: moveData[0],
            white_distro: moveData[1],
            white_move_ml: moveData[2],
            white_distro_ml: moveData[3],
            black_move: moveData[4],
            black_distro: moveData[5],
            black_move_ml: moveData[6],
            black_distro_ml: moveData[7],
        })
    }

    render() {
        return (

            <div className="ui bottom attached segment pushable">
                <div className="ui visible inverted left vertical sidebar menu">
                    <br />
                    <div class="ui medium yellow header">System Messages</div>
                    <br />
                    <p style={{ color: "lightyellow" }}>
                        {this.state.message4}
                    </p>
                    <p style={{ color: "lightgrey" }}>
                        {this.state.message3}
                    </p>
                    <p style={{ color: "darkgrey" }}>
                        {this.state.message2}
                    </p>
                    <p style={{ color: "grey" }}>
                        {this.state.message1}
                    </p>

                    <br />
                    <p style={{ color: "grey" }}>
                        {this.state.message1}
                    </p>
                    <div class="ui medium olive header">Move Recommendations</div>

                    <div class="ui small message red">
                        <div class="ui list" >
                            <div class="item" style={{ color: "red" }}><b>Pressure Move:</b> {this.state.black_move}</div>
                            <div class="item" style={{ color: "red" }}><b>Pressure Result:</b> {this.state.black_distro}</div>
                            <div class="item" style={{ color: "red" }}><b>ML Move:</b> {this.state.black_move_ml}</div>
                            <div class="item" style={{ color: "red" }}><b>ML Rating:</b> {this.state.black_distro_ml}</div>
                        </div>
                    </div>
                    <div class="ui small message teal">
                        <div class="ui list" >
                            <div class="item" style={{ color: "blue" }}><b>Pressure Move:</b>  {this.state.white_move}</div>
                            <div class="item" style={{ color: "blue" }}><b>Pressure Result:</b> {this.state.white_distro}</div>
                            <div class="item" style={{ color: "blue" }}><b>ML Move:</b> {this.state.white_move_ml}</div>
                            <div class="item" style={{ color: "blue" }}><b>ML Rating:</b> {this.state.white_distro_ml}</div>
                        </div>
                    </div>

                </div>


                <div className="pusher">
                    <div className="ui basic segment">
                        <h3 className="ui header">Chess Pressure Tool</h3>
                        <div className="ui container" style={{ margin: '10px' }}>
                            <Board updateMessage={this.updateMessage} updateMoves={this.updateMoves} />
                        </div>
                    </div>
                </div>
            </div>


        )
    }
}

export default App;