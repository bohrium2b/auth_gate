import {useState} from 'react';
import {Button,Accordion,AccordionDetails,AccordionSummary,TextField, Box} from '@mui/material';


type OAuthProvider = {
    name: string;
    url: string;
    clientId: string;
    clientSecret: string;
    endpoints: {
        userinfo: string;
        authorize: string;
        accessToken: string;
    }

}

type Configuration = {
    providers: OAuthProvider[];
    redirectUri: string;
}

export const Configurator = () => {
    const [configuration, setConfiguration] = useState<Configuration>({providers: [], redirectUri: ''})
    const save = () => {
        fetch('/configure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(configuration)
        })
    }
    return (
        <>
            <Box sx={{padding: '1rem'}}>
            <TextField label="Redirect URI" value={configuration.redirectUri} onChange={e => setConfiguration({...configuration, redirectUri: e.target.value})} /> <br />
            </Box>
            <Box sx={{padding: '1rem'}}>
            {configuration.providers.map((provider, index) => (
                <Accordion key={index}>
                    <AccordionSummary>
                        {provider.name}
                    </AccordionSummary>
                    <AccordionDetails>
                        <Box sx={{width: '50%'}}></Box>
                        <TextField label="Name" value={provider.name} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, name: e.target.value}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="URL" value={provider.url} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, url: e.target.value}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="Client ID" value={provider.clientId} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, clientId: e.target.value}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="Client Secret" value={provider.clientSecret} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, clientSecret: e.target.value}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="Userinfo Endpoint" value={provider.endpoints.userinfo} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, endpoints: {...provider.endpoints, userinfo: e.target.value}}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="Authorize Endpoint" value={provider.endpoints.authorize} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, endpoints: {...provider.endpoints, authorize: e.target.value}}, ...configuration.providers.slice(index + 1)]})} /> <br />
                        <TextField label="Access Token Endpoint" value={provider.endpoints.accessToken} onChange={e => setConfiguration({...configuration, providers: [...configuration.providers.slice(0, index), {...provider, endpoints: {...provider.endpoints, accessToken: e.target.value}}, ...configuration.providers.slice(index + 1)]})} /> <br />
                    </AccordionDetails>
                </Accordion>
            ))}
            </Box>
            <Box sx={{padding: '1rem'}}>
            <Button onClick={() => setConfiguration({...configuration, providers: [...configuration.providers, {name: 'New Provider', url: '', clientId: '', clientSecret: '', endpoints: {userinfo: '', authorize: '', accessToken: ''}}]})}>Add Provider</Button> <Button onClick={save}>Save</Button>
            </Box>
        </>
    )
}