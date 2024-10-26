import ErrorBlock from "../components/ui/ErrorBlock";

const Error = ({error}) => {

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            <div className="flex flex-grow flex-col justify-center items-center p-8">
                <ErrorBlock>{error}</ErrorBlock>
            </div>
        </div>
    );
};

export default Error;
